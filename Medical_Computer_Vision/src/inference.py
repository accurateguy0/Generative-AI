import os
from PIL import Image
import torch
import matplotlib.pyplot as plt
# ten plik zajmuje się podzieleniem dużego testowego obrazka na małe części 64x64
def slice_and_detect(image_path, model, transform, info, stride=64):
    # 1. Stwórz folder outputowy
    output_dir = "sliced_cells"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Wczytaj duży obraz
    big_img = Image.open(image_path).convert('RGB')
    width, height = big_img.size
    print(f"Original Image Size: {width}x{height}")

    # 3. logika rozmiaru
    window_size = 64
    count = 0
    
    # dla zapisania rezultatów
    results = []

    model.eval()
    with torch.no_grad():
        for y in range(0, height - window_size + 1, stride):
            for x in range(0, width - window_size + 1, stride):
                # definiowanie pudełka do przekroju
                box = (x, y, x + window_size, y + window_size)
                slice_img = big_img.crop(box)

                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # Preprocess for the AI
                img_t = transform(slice_img).unsqueeze(0).to(device)
                
                # przewiduj
                output = model(img_t)
                probs = torch.nn.functional.softmax(output, dim=1)
                conf, pred = torch.max(probs, 1)
                
                class_name = info['label'][str(pred.item())]
                confidence = conf.item()

                # zapisz to w dysku
                slice_name = f"slice_{y}_{x}_{class_name}.jpg"
                slice_img.save(os.path.join(output_dir, slice_name))
                
                # Jeśli pewność jest wysoka, zatrzymuj dla wizualizacji
                if confidence > 0.8:
                    results.append((slice_img, class_name, confidence))
                
                count += 1

    print(f"Finished! Created {count} slices in the '{output_dir}' folder.")
    return results

# --- Jak uruchomić ---
# samples = slice_and_detect('obraz.jpg', model, transform, info)

# Opcjonalne pokaż 10 wysoko pewnościowych obrazków
def show_detections(results):
    plt.figure(figsize=(15, 6))
    for i, (img, name, conf) in enumerate(results[:10]):
        plt.subplot(2, 5, i+1)
        plt.imshow(img)
        plt.title(f"{name}\n{conf*100:.1f}%")
        plt.axis('off')
    plt.show()

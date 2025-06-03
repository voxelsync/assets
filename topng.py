import os
import glob
from PIL import Image
import cairosvg

def convert_svg_to_png(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    svg_files = glob.glob(os.path.join(input_folder, '**/*.svg'), recursive=True)
    
    target_sizes = [2048, 1024, 512, 248, 32, 16]
    
    for svg_path in svg_files:
        try:
            with open(svg_path, 'rb') as f:
                svg_data = f.read()
            
            base_name = os.path.splitext(os.path.basename(svg_path))[0]
            
            temp_png = os.path.join(output_folder, f'temp_{base_name}.png')
            cairosvg.svg2png(bytestring=svg_data, write_to=temp_png)
            
            with Image.open(temp_png) as img:
                original_width, original_height = img.size
                aspect_ratio = original_height / original_width
                
                for size in target_sizes:
                    new_height = int(size * aspect_ratio)
                    
                    resized_img = img.resize((size, new_height), Image.Resampling.LANCZOS)
                    
                    output_name = f"{base_name}-{size}x.png"
                    output_path = os.path.join(output_folder, output_name)
                    resized_img.save(output_path, 'PNG')
            
            os.remove(temp_png)
            print(f"Verarbeitet: {svg_path} -> {len(target_sizes)} PNGs")
            
        except Exception as e:
            print(f"Fehler bei {svg_path}: {str(e)}")

if __name__ == "__main__":
    input_folder = input("Pfad zum Eingabeordner mit SVGs: ")
    output_folder = os.path.join(input_folder, "api")
    
    convert_svg_to_png(input_folder, output_folder)
    print("Konvertierung abgeschlossen!")
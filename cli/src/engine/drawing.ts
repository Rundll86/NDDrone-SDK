import { JimpInstance } from "jimp";

export function drawRect(image: JimpInstance, x: number, y: number, width: number, height: number, color: number) {
    for (let i = x; i < x + width; i++) {
        for (let j = y; j < y + height; j++) {
            image.setPixelColor(color, i, j);
        }
    }
}
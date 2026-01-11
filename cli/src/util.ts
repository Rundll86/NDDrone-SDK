import path from "path";
import fs from "fs/promises";

export async function copyDirectory(src: string, dest: string) {
    const entries = await fs.readdir(src, { withFileTypes: true });
    await fs.mkdir(dest, { recursive: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            await copyDirectory(srcPath, destPath);
        } else {
            await fs.copyFile(srcPath, destPath);
        }
    }
}
export async function isExist(path: string) {
    try {
        await fs.access(path);
        return true;
    } catch (error) {
        return false;
    }
}
export async function isFile(path: string) {
    const stats = await fs.stat(path);
    return stats.isFile();
}
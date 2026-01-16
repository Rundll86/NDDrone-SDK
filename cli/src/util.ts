import path from "path";
import fs from "fs/promises";
import EventEmitter from "events";
import readline from "readline/promises";

export async function copyDirectory(src: string, dest: string, mapFile?: (srcPath: string, destPath: string) => string) {
    const entries = await fs.readdir(src, { withFileTypes: true });
    await fs.mkdir(dest, { recursive: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            await copyDirectory(srcPath, destPath, mapFile);
        } else {
            const newDestPath = mapFile ? mapFile(srcPath, destPath) : destPath;
            await fs.copyFile(srcPath, newDestPath);
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
export async function input(prompt: string) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    const result = await rl.question(prompt);
    rl.close();
    return result;
}
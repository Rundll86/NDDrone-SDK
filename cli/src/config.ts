import { parse } from "ini";
import fs from "fs/promises";

export async function loadConfig(): Promise<ConfigData> {
    const configText = await fs.readFile("config.ini", "utf-8");
    return parse(configText) as ConfigData;
}
export interface ConfigData {
    runtime: {
        path: string;
    };
    build: {
        debug: boolean;
    }
}
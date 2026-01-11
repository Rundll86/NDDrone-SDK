import { parse } from "ini";
import fs from "fs/promises";
import { isExist, isFile } from "./util";

export async function loadConfig(): Promise<ConfigData> {
    const configText = await fs.readFile("config.ini", "utf-8");
    const result = parse(configText) as ConfigData;
    if (typeof result.build.debug !== "boolean") {
        console.error("debug选项必须为布尔值");
        process.exit(1);
    }
    result.frames.count = Number(result.frames.count);
    if (isNaN(result.frames.count)) {
        console.error("frames.count选项必须为数字");
        process.exit(1);
    }
    if (!await isExist(result.runtime.path)) {
        console.log("runtime.path不存在");
        process.exit(1);
    }
    if (await isFile(result.runtime.path)) {
        console.log("runtime.path必须为目录");
        process.exit(1);
    }
    return result;
}
export interface ConfigData {
    runtime: {
        path: string;
    };
    frames: {
        count: number;
    },
    build: {
        debug: boolean;
    };
}
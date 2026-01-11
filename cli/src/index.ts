import { program } from "commander";
import { ConfigData, loadConfig } from "./config";
import path from "path";
import { copyDirectory } from "./util";
import chokidar from "chokidar";
import process from "process";
import childProcess from "child_process";
import fs from 'fs/promises';

async function build(config: ConfigData) {
    await copyDirectory(path.resolve("src"), config.runtime.path);
    await fs.rename(path.resolve(config.runtime.path, "flymode.py"), path.resolve(config.runtime.path, "Drone_psycho.py"));
}
async function main() {
    const config = await loadConfig();
    program
        .name("NDDrone")
        .version("1.0.0");

    program.command("build")
        .option("-w, --watch", "是否开启视奸模式", false)
        .option("-g, --generate", "是否编译刺激块", false)
        .action(async (options: { watch: boolean, generate: boolean }) => {
            if (options.watch) {
                const watcher = chokidar.watch(path.resolve("src"));
                watcher.on("change", () => build(config));
                watcher.on("add", () => build(config));
                watcher.on("unlink", () => build(config));
                watcher.on("ready", () => process.stdout.write("正在视奸工作区..."));
            } else {
                await build(config);
                process.stdout.write("工作区编译完成\n");
            }
            if (options.generate) {
                console.log("正在编译刺激块...");
                program.parseAsync(["generate"], { from: "user" });
            }
        });
    program.command("generate")
        .action(async () => {
            try {
                childProcess.execSync("python cli/generator/generate.py", { stdio: "inherit" });
            } catch { }
        });

    program.parse(process.argv);
}
main();
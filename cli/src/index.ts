import { program } from "commander";
import { loadConfig } from "./config";
import path from "path";
import { copyDirectory } from "./util";
import chokidar from "chokidar";
import process from "process";

async function main() {
    const config = await loadConfig();
    program
        .name("NDDrone")
        .version("1.0.0");

    program.command("build")
        .option("-w, --watch", undefined, false)
        .action(async (options: { watch: boolean }) => {
            if (options.watch) {
                const watcher = chokidar.watch(path.resolve("src"));
                watcher.on("change", async () => {
                    await copyDirectory(path.resolve("src"), config.runtime.path);
                });
                watcher.on("add", async () => {
                    await copyDirectory(path.resolve("src"), config.runtime.path);
                });
                watcher.on("unlink", async () => {
                    await copyDirectory(path.resolve("src"), config.runtime.path);
                });
                watcher.on("ready", () => process.stdout.write("正在视奸工作区..."));
            } else {
                await copyDirectory(path.resolve("src"), config.runtime.path);
                process.stdout.write("编译成功\n");
            }
        });

    program.parse(process.argv);
}
main();
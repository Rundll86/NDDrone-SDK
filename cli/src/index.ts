import { program } from "commander";
import { ConfigData, loadConfig } from "./config";
import path from "path";
import { copyDirectory, input } from "./util";
import chokidar from "chokidar";
import process from "process";
import childProcess from "child_process";
import packageData from "../../package.json";
import { CommandServer } from "./servers/command";

async function build(config: ConfigData) {
    await copyDirectory(
        path.resolve("src"),
        config.runtime.path,
        (src, dest) => path.basename(src) === "flymode.py" ? path.join(path.dirname(dest), "Drone_psycho.py") : dest
    );
}
async function main() {
    const config = await loadConfig();
    program
        .name(packageData.name)
        .version(packageData.version);

    program.command("build")
        .option("-w, --watch", "是否开启视奸模式", false)
        .option("-g, --generate", "是否编译刺激块", false)
        .action(async (options: { watch: boolean, generate: boolean }) => {
            if (options.watch) {
                const watcher = chokidar.watch(path.resolve("src"));
                for (const event of ["change", "add", "unlink"] as const) {
                    watcher.on(event, () => build(config));
                }
                watcher.on("ready", () => process.stdout.write("正在视奸工作区..."));
            } else {
                console.log("正在编译工作区...");
                await build(config);
                console.log("工作区编译完成");
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
                console.log("刺激块编译完成");
            } catch {
                console.error("刺激块编译失败");
            }
        });

    program.command("command")
        .action(async () => {
            console.log("--- NDDrone-SDK 无人机交互终端 ---");
            process.stdout.write("正在连接无人机...");
            const commandServer = new CommandServer();
            commandServer.send("command");
            try {
                const response = await commandServer.waitMessage(5000);
                if (response !== "ok") {
                    throw new Error("响应无效");
                }
            } catch (err) {
                if (err instanceof Error) {
                    console.error(`连接失败：${err.message}，请确保无人机已开启并连接至局域网。`);
                } else {
                    console.error("发生未知错误。")
                };
            }
            console.log("连接成功。");
            while (true) {
                try {
                    const cmd = await input("> ");
                    console.log(cmd);
                } catch (err) {
                    if (err instanceof Error) {
                        if (err.message.startsWith("Aborted")) {
                            process.exit(0);
                        }
                        console.error(err.message);
                    }
                }
            }
        });

    program.parse(process.argv);
}
main();
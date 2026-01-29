import { program } from "commander";
import { ConfigData, loadConfig } from "./config";
import path from "path";
import { copyDirectory, input } from "./util";
import chokidar from "chokidar";
import process from "process";
import childProcess from "child_process";
import packageData from "../../package.json";
import { CommandServer } from "./servers/command";
import { DroneStateServer } from "./servers/droneState";
import { PingServer } from "./servers/ping";

async function main() {
    const config = await loadConfig();
    program
        .name(packageData.name)
        .version(packageData.version);

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
            const pingServer = new PingServer();
            await pingServer.doOnce();
            console.log("连接成功。");
            while (true) {
                try {
                    commandServer.send(await input("> "));
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
    program.command("state")
        .option("-w, --watch", "是否持续视奸无人机状态", false)
        .action(async (options: { watch: boolean }) => {
            const droneState = new DroneStateServer();
            await droneState.initialize();
            do {
                console.log(droneState.toString());
            } while (options.watch);
        });

    program.parse(process.argv);
}
main();

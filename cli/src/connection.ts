import dgram from "dgram";
import { Address } from "./constants";

export interface Oncable extends DroneServer {
    doOnce(): Promise<void>;
}
export interface Initializable extends DroneServer {
    initialize(): Promise<void>;
}
export abstract class DroneServer {
    socket: dgram.Socket;
    remoteAddress?: Address;
    selfAddress?: Address;

    lastReceiveTime: number = 0;
    constructor(type: dgram.SocketType, remoteAddress?: Address, selfAddress?: Address) {
        this.socket = dgram.createSocket(type);
        this.remoteAddress = remoteAddress;
        this.selfAddress = selfAddress;
        if (selfAddress) {
            const [host, port] = selfAddress;
            this.socket.bind(port, host);
        }
        this.socket.on("message", (msg, rinfo) => {
            this.lastReceiveTime = Date.now();
            this.receive(msg.toString(), rinfo);
        });
    }
    abstract receive(message: string, remote: dgram.RemoteInfo): void;
    async send(message: string, address?: Address): Promise<void> {
        return new Promise((resolve, reject) => {
            const addr = address ?? this.remoteAddress;
            if (!addr) {
                reject(new Error("未提供远程地址"));
                return;
            }
            const [host, port] = addr;
            this.socket.send(Buffer.from(message), port, host, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });
    }
    async waitMessage(timeout: number): Promise<string> {
        return new Promise((resolve, reject) => {
            let timeouted = false;
            const timer = setTimeout(() => {
                timeouted = true;
                reject(new Error("响应超时"));
            }, timeout);
            this.socket.once("message", (message) => {
                clearTimeout(timer);
                if (!timeouted) resolve(message.toString());
            });
        });
    }
    protected async polling<T>(callback: (
        stop: (result?: T) => void,
        round: number,
        runningTime: number
    ) => void, interval: number): Promise<T | undefined> {
        return new Promise((resolve) => {
            let round = 0;
            const startTime = Date.now();
            const timer = setInterval(
                () => callback((result) => {
                    clearInterval(timer);
                    resolve(result);
                }, round++, Date.now() - startTime),
                interval
            );
        });
    }
}
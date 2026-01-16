import { DroneServer } from "../connection";

export class CommandServer extends DroneServer {
    constructor() {
        super("udp4", ["192.168.10.1", 8889]);
    }
    receive(message: string): void {
        console.log(message);
    }
}
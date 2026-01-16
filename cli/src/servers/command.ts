import { DroneServer } from "../connection";
import { DRONE_ADDRESS } from "../constants";

export class CommandServer extends DroneServer {
    constructor() {
        super("udp4", DRONE_ADDRESS);
    }
    receive(message: string): void {
        console.log(`Drone: ${message}`);
    }
}
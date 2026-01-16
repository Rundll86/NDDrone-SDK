import { RemoteInfo, Socket } from "node:dgram";
import { DroneServer } from "../connection";

export interface DroneState {
    mid: number;
    x: number;
    y: number;
    z: number;
    mpry: [number, number, number];
    pitch: number;
    roll: number;
    yaw: number;
    vgx: number;
    vgy: number;
    vgz: number;
    templ: number;
    temph: number;
    tof: number;
    h: number;
    bat: number;
    baro: number;
}
export class DroneStateServer extends DroneServer {
    currentState: DroneState | null = null;
    constructor() {
        super("udp4", undefined, ["0.0.0.0", 8890]);
    }
    receive(message: string): void {
        const state: Record<string, number | number[]> = {};
        for (const pair in message.trim().split(";").filter(Boolean)) {
            const [key, value] = pair.split(":");
            if (key in ["mpry"]) {
                state.mpry = value.split(",").map(Number);
            } else {
                state[key] = Number(value);
            }
        }
        this.currentState = state as unknown as DroneState;
    }
}
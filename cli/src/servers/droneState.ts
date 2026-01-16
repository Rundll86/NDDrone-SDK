import { DroneServer, Initializable } from "../connection";
import { STATE_SERVER_ADDRESS } from "../constants";

export interface DroneState {
    mid: number,
    x: number,
    y: number,
    z: number,
    mpry: [number, number, number],
    pitch: number,
    roll: number,
    yaw: number,
    vgx: number,
    vgy: number,
    vgz: number,
    templ: number,
    temph: number,
    tof: number,
    h: number,
    bat: number,
    baro: number,
    time: number,
    agx: number,
    agy: number,
    agz: number,
}
export const vectorArrayKeys = ["mpry"];
export const keyMap: Record<string, string> = {
    mid: "挑战卡ID",
    x: "X轴坐标",
    y: "Y轴坐标",
    z: "Z轴坐标",
    mpry: "挑战卡三向角度",
    pitch: "俯仰角度",
    roll: "横滚角度",
    yaw: "偏航角度",
    vgx: "X轴速度",
    vgy: "Y轴速度",
    vgz: "Z轴速度",
    templ: "主板最低温度",
    temph: "主板最高温度",
    tof: "ToF距离",
    h: "起飞高度",
    bat: "剩余电量",
    baro: "气压高度",
    time: "电机运行时间",
    agx: "X轴加速度",
    agy: "Y轴加速度",
    agz: "Z轴加速度",
};
export class DroneStateServer extends DroneServer implements Initializable {
    current: DroneState | null = null;
    constructor() {
        super("udp4", undefined, STATE_SERVER_ADDRESS);
    }
    receive(message: string): void {
        const state: Record<string, number | number[]> = {};
        for (const pair in message.trim().split(";").filter(Boolean)) {
            const [key, value] = pair.split(":");
            if (vectorArrayKeys.includes(key)) {
                state[key] = value.split(",").map(Number);
            } else {
                state[key] = Number(value);
            }
        }
        this.current = state as unknown as DroneState;
    }
    toString() {
        return Object.entries(this.current ?? {}).map(([key, value]: [string, number]) => `${keyMap[key]}：${value}`).join(",\n");
    }
    async initialize(): Promise<void> {
        await this.polling((stop) => this.current && stop(), 500);
    }
}
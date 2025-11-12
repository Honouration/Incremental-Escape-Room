export enum ActionType {
  MAIN = "main",
  OPTIONAL = "optional",
  RISK = "risk",
}

export interface Action {
  id: string;
  description: string;
  turnCost: number;
  type: ActionType;
  requires?: string[]; // prerequisite action IDs
  rewards?: string[]; // items added to inventory
  unlocks?: string; // room transition or secret unlock
  consequence?: {
    type: "turnLoss" | "item" | "secret";
    value: string | number;
  };
}

export interface Room {
  id: number;
  name: string;
  theme: string;
  description: string;
  mainActions: Action[];
  optionalActions: Action[];
  riskActions: Action[];
  nextRoom?: number;
}

export interface RoomState {
  room: Room;
  discovered: string[];
  failed: boolean;
}

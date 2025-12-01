"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.clockTower = void 0;
const roomTypes_1 = require("./roomTypes");
exports.clockTower = {
    id: 5,
    name: "Clock Tower / Final Escape Chamber",
    theme: "Time, culmination",
    description: "Massive gears surround you. The clock ticks loudly. Time is running out.",
    mainActions: [
        {
            id: "clock_inspect_clock",
            description: "Inspect main clock mechanism",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            rewards: ["clock_revealed"],
        },
        {
            id: "clock_input_sequence_1",
            description: "Input first diary sequence",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_inspect_clock", "diary_page_1"],
        },
        {
            id: "clock_input_sequence_2",
            description: "Input second diary sequence",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_input_sequence_1", "diary_page_2"],
        },
        {
            id: "clock_input_sequence_3",
            description: "Complete final diary sequence",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_input_sequence_2", "diary_page_3"],
            rewards: ["clock_unlocked"],
        },
        {
            id: "clock_wind_gears",
            description: "Wind the gears",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_input_sequence_3"],
        },
        {
            id: "clock_activate_pendulum",
            description: "Activate pendulum mechanism",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_wind_gears"],
        },
        {
            id: "clock_final_puzzle",
            description: "Solve final mini-puzzle",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_activate_pendulum"],
            rewards: ["escape_code"],
        },
        {
            id: "clock_escape",
            description: "Open final door and ESCAPE!",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["clock_final_puzzle"],
            unlocks: "ESCAPE",
        },
    ],
    optionalActions: [
        {
            id: "clock_hidden_panel",
            description: "Find hidden panel (secret ending)",
            turnCost: 3,
            type: roomTypes_1.ActionType.OPTIONAL,
            requires: ["clock_inspect_clock"],
            unlocks: "secret_ending",
        },
        {
            id: "clock_pendulum_puzzle",
            description: "Solve pendulum extra puzzle (Easter egg)",
            turnCost: 3,
            type: roomTypes_1.ActionType.OPTIONAL,
            requires: ["clock_activate_pendulum"],
        },
        {
            id: "clock_collect_items",
            description: "Collect hidden items for cinematic ASCII ending",
            turnCost: 1,
            type: roomTypes_1.ActionType.OPTIONAL,
            requires: ["clock_final_puzzle"],
            rewards: ["cinematic_trigger"],
        },
    ],
    riskActions: [
        {
            id: "clock_wrong_sequence",
            description: "Input wrong sequence (gears jam)",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 2 },
        },
        {
            id: "clock_ignore_clues",
            description: "Ignore diary clues (must retry)",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 2 },
        },
    ],
};
//# sourceMappingURL=room5.js.map
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.forgottenAttic = void 0;
const roomTypes_1 = require("./roomTypes");
exports.forgottenAttic = {
    id: 4,
    name: "Forgotten Attic",
    theme: "Memory, history",
    description: "Cobwebs and dust cover everything. Old portraits watch from the walls.",
    mainActions: [
        {
            id: "attic_inspect_portraits",
            description: "Inspect portraits for old key",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            rewards: ["old_key"],
        },
        {
            id: "attic_open_trunks",
            description: "Open trunks and find diary pages",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["attic_inspect_portraits"],
            rewards: ["diary_page_1", "diary_page_2", "diary_page_3"],
        },
        {
            id: "attic_solve_numeric_puzzle",
            description: "Solve numeric mini-puzzle",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["attic_open_trunks"],
            rewards: ["puzzle_solution"],
        },
        {
            id: "attic_examine_corners",
            description: "Examine corners for hidden symbols",
            turnCost: 2,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["attic_solve_numeric_puzzle"],
        },
        {
            id: "attic_unlock_ladder",
            description: "Unlock secret ladder to Room 5",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["attic_examine_corners", "old_key"],
            unlocks: "5",
        },
    ],
    optionalActions: [
        {
            id: "attic_extra_trunk",
            description: "Open extra trunk (secret map)",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            requires: ["attic_open_trunks"],
            rewards: ["detailed_map"],
        },
        {
            id: "attic_dust_piles",
            description: "Search dust piles for hidden item",
            turnCost: 1,
            type: roomTypes_1.ActionType.OPTIONAL,
        },
        {
            id: "attic_rearrange_items",
            description: "Rearrange items for secret clue",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["final_clue"],
        },
    ],
    riskActions: [
        {
            id: "attic_ladder_fall",
            description: "Fall from ladder",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 1 },
        },
        {
            id: "attic_drop_diary",
            description: "Drop diary pages",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 1 },
        },
        {
            id: "attic_miss_clue",
            description: "Miss numeric clue (retry)",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 1 },
        },
    ],
    nextRoom: 5,
};
//# sourceMappingURL=room4.js.map
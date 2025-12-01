"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.abandonedLibrary = void 0;
const roomTypes_1 = require("./roomTypes");
exports.abandonedLibrary = {
    id: 2,
    name: "Abandoned Library",
    theme: "Knowledge, riddles",
    description: "Floor-to-ceiling bookshelves surround you. The air smells of aged paper and mystery.",
    mainActions: [
        {
            id: "lib_inspect_bookshelves",
            description: "Inspect bookshelves for riddle note",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            rewards: ["riddle_note"],
        },
        {
            id: "lib_examine_desk",
            description: "Examine desk",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            rewards: ["magnifying_glass"],
        },
        {
            id: "lib_solve_riddle",
            description: "Solve multi-step riddle",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lib_inspect_bookshelves", "lib_examine_desk"],
            rewards: ["hatch_combo"],
        },
        {
            id: "lib_examine_additional_shelves",
            description: "Examine additional shelves for numeric clues",
            turnCost: 2,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lib_solve_riddle"],
        },
        {
            id: "lib_highlight_letters",
            description: "Highlight hidden letters in books",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lib_examine_additional_shelves"],
        },
        {
            id: "lib_open_hatch",
            description: "Open hatch and move to Room 3",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lib_highlight_letters", "hatch_combo"],
            unlocks: "3",
        },
    ],
    optionalActions: [
        {
            id: "lib_hidden_drawer",
            description: "Find hidden drawer with amulet",
            turnCost: 1,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["amulet"],
        },
        {
            id: "lib_rearrange_books",
            description: "Rearrange books to reveal secret passage",
            turnCost: 3,
            type: roomTypes_1.ActionType.OPTIONAL,
        },
        {
            id: "lib_inspect_maps",
            description: "Inspect maps (clue for Room 5)",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["clock_tower_clue"],
        },
        {
            id: "lib_hidden_letter_codes",
            description: "Decode hidden letter patterns",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
        },
        {
            id: "lib_open_cabinet",
            description: "Open locked cabinet",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["ancient_scroll"],
        },
    ],
    riskActions: [
        {
            id: "lib_wrong_riddle",
            description: "Attempt wrong riddle solution",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 2 },
        },
        {
            id: "lib_ignore_magnifying_glass",
            description: "Ignore magnifying glass clues",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 2 },
        },
    ],
    nextRoom: 3,
};
//# sourceMappingURL=room2.js.map
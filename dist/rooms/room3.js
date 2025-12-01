"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.secretLaboratory = void 0;
const roomTypes_1 = require("./roomTypes");
exports.secretLaboratory = {
    id: 3,
    name: "Secret Laboratory",
    theme: "Science, danger",
    description: "Strange equipment lines the walls. Chemical odors burn your nostrils.",
    mainActions: [
        {
            id: "lab_inspect_panel",
            description: "Inspect control panel",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            rewards: ["panel_code_1"],
        },
        {
            id: "lab_sequence_step1",
            description: "Input first sequence (control panel)",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_inspect_panel"],
        },
        {
            id: "lab_sequence_step2",
            description: "Input second sequence (control panel)",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_sequence_step1"],
        },
        {
            id: "lab_sequence_step3",
            description: "Complete sequence (control panel)",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_sequence_step2"],
            rewards: ["panel_unlocked"],
        },
        {
            id: "lab_examine_chemicals",
            description: "Examine chemical shelves",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_inspect_panel"],
        },
        {
            id: "lab_combine_chemicals",
            description: "Combine 3 chemicals (puzzle)",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_examine_chemicals"],
            rewards: ["mixture"],
        },
        {
            id: "lab_test_mixture",
            description: "Test mixture in beaker",
            turnCost: 3,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_combine_chemicals"],
            rewards: ["tested_mixture"],
        },
        {
            id: "lab_unlock_chest",
            description: "Unlock chest with critical item",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_sequence_step3"],
            rewards: ["crystal_key"],
        },
        {
            id: "lab_open_door",
            description: "Open door to Room 4",
            turnCost: 1,
            type: roomTypes_1.ActionType.MAIN,
            requires: ["lab_unlock_chest"],
            unlocks: "4",
        },
    ],
    optionalActions: [
        {
            id: "lab_hidden_button",
            description: "Find hidden button (ASCII cosmetic)",
            turnCost: 1,
            type: roomTypes_1.ActionType.OPTIONAL,
        },
        {
            id: "lab_extra_chemical",
            description: "Discover secret chemical combo",
            turnCost: 3,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["secret_potion"],
        },
        {
            id: "lab_rearrange_equipment",
            description: "Rearrange lab equipment (Easter egg)",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
        },
        {
            id: "lab_inspect_drawers",
            description: "Inspect lab drawers for documents",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["hidden_document"],
        },
        {
            id: "lab_secret_compartment",
            description: "Find secret compartment",
            turnCost: 2,
            type: roomTypes_1.ActionType.OPTIONAL,
            rewards: ["bonus_vial"],
        },
    ],
    riskActions: [
        {
            id: "lab_wrong_sequence",
            description: "Input wrong sequence (sparks fly)",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 2 },
        },
        {
            id: "lab_wrong_mixture",
            description: "Wrong chemical mixture (minor explosion)",
            turnCost: 0,
            type: roomTypes_1.ActionType.RISK,
            consequence: { type: "turnLoss", value: 1 },
        },
    ],
    nextRoom: 4,
};
//# sourceMappingURL=room3.js.map
import * as readline from "readline";
import { GameManager } from "./gameManager";
import { GameUI } from "./ui";

export class GameLoop {
  private manager: GameManager;
  private rl: readline.Interface;
  private running: boolean = true;

  constructor() {
    this.manager = new GameManager();
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
  }

  async start(): Promise<void> {
    GameUI.displayWelcome();
    await this.delay(2000);

    while (this.running && !this.manager.isGameOver()) {
      this.displayCurrentState();
      await this.promptUserAction();
    }

    if (this.manager.isGameOver()) {
      GameUI.displayGameOver(this.manager.getGameState());
    }

    this.rl.close();
  }

  private displayCurrentState(): void {
    const room = this.manager.getCurrentRoom();
    const state = this.manager.getGameState();

    GameUI.displayRoom(room);
    GameUI.displayGameState(state);

    const availableActions = this.manager.getAvailableActions();
    GameUI.displayActions(availableActions);
  }

  private async promptUserAction(): Promise<void> {
    return new Promise((resolve) => {
      this.rl.question("Enter command (0-9, 'inventory', 'status', 'help', 'quit'): ", (input) => {
        this.handleInput(input.trim().toLowerCase());
        resolve();
      });
    });
  }

  private handleInput(input: string): void {
    if (input === "quit") {
      this.running = false;
      console.log("👋 Thanks for playing!\n");
      return;
    }

    if (input === "help") {
      GameUI.displayHelp();
      return;
    }

    if (input === "inventory") {
      const inventory = this.manager.getInventory();
      console.log(
        `\n📦 Inventory: ${inventory.length > 0 ? inventory.join(", ") : "Empty"}\n`
      );
      return;
    }

    if (input === "status") {
      const state = this.manager.getGameState();
      console.log(`\n📊 Current Status:`);
      console.log(`  Room: ${state.currentRoom}/5`);
      console.log(`  Turns: ${state.totalTurns}`);
      console.log(`  Items: ${state.inventory.length}`);
      console.log(`  Secrets: ${state.discoveredSecrets.size}\n`);
      return;
    }

    // Handle action selection
    const actionIndex = parseInt(input, 10);
    if (!isNaN(actionIndex)) {
      const availableActions = this.manager.getAvailableActions();

      if (actionIndex < 0 || actionIndex >= availableActions.length) {
        console.log("❌ Invalid action number.\n");
        return;
      }

      const action = availableActions[actionIndex];
      const result = this.manager.performAction(action.id);
      GameUI.displayActionResult(result);

      // Check if player ran out of turns
      if (this.manager.getTurnsRemaining() <= 0 && !this.manager.getGameState().escaped) {
        console.log("⏰ TIME'S UP! You ran out of turns!\n");
        this.running = false;
      }

      return;
    }

    console.log("❌ Invalid command. Type 'help' for options.\n");
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

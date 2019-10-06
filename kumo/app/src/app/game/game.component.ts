import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { DatabaseService } from '../database.service';
import { ConfirmationService } from 'primeng/api';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  @Input() game: any;
  @Output() refreshGameData = new EventEmitter();

  public selectedSeatedPlayer;
  public get seatedPlayers() {
    let ret = [];
    for (let i = 0; i < this.game.players.length && i < this.game.seats; ++i) {
      ret.push({label: this.game.players[i].name, value: {id: this.game.players[i].id, name: this.game.players[i].name}});
    }

    return ret;
  }

  public selectedWaitingPlayer;
  public get waitingPlayers() {
    let ret = [];
    for (let i = this.game.seats; i < this.game.players.length; ++i) {
      ret.push({label: this.game.players[i].name, value: {id: this.game.players[i].id, name: this.game.players[i].name}});
    }

    return ret;
  }

  public registered = false;
  public displayDetails = false;

  public get gameSystem() {
    if (this.game.system.name === 'D&D' ||
        this.game.system.name === 'Shadowrun' ||
        this.game.system.name === 'Pathfinder' ||
        this.game.system.name === 'Starfinder' ||
        this.game.system.name === 'DCC' ||
        this.game.system.name === 'MLP') {
      return this.game.system.name;
    }

    return 'Other';
  }

  constructor(private db: DatabaseService,
    private confirmationService: ConfirmationService) {
      setTimeout(() => this.checkRegistration(), 500);
    }

  ngOnInit() {
  }

  public checkRegistration() {
    this.db.isRegistered(this.game.id).subscribe(
      (success2: any) => {
        console.log(success2);
        if (success2.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: success2.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          if (success2.hasOwnProperty('registered')) {
            this.registered = success2.registered;
          } else {
            this.confirmationService.confirm({
              header: 'Error',
              message: 'Unable to determine registered status',
              icon: 'pi pi-exclamation-triangle',
              accept: () => {}
            });
          }
        }
      },
      (failure) => {
        console.error(failure);

        if (failure.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: failure.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          this.confirmationService.confirm({
            header: 'Error',
            message: 'Unknown error',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      },
      () => {

      }
    );
  }

  public refreshGame() {
    this.db.getGameById(this.game.id).subscribe(
      (success: any) => {
        console.log(success);
        if (success.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: success.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          this.game = success.results[0];
          this.checkRegistration();
        }
      }, (failure) => {
        console.error(failure);

        if (failure.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: failure.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          this.confirmationService.confirm({
            header: 'Error',
            message: 'Unknown error',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }

      }, () => {
        this.refreshGameData.emit(this.game);
      }
    );
  }

  public register() {
    this.db.registerForGame(this.game.id).subscribe(
      (success: any) => {
        console.log(success);
        if (success.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: success.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else if (success.hasOwnProperty('success') && success.success === true) {
          this.confirmationService.confirm({
            header: 'Success!',
            icon: '',
            message: 'You have been registered!',
            accept: () => {}
          });
        } else {
          this.confirmationService.confirm({
            header: 'Error',
            message: 'Unknown error',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      }, (failure) => {
        console.error(failure);

        if (failure.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: failure.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          this.confirmationService.confirm({
            header: 'Error',
            message: 'Unknown error',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      }, () => {
        this.refreshGame();
      }
    );
  }

  public deRegister() {
    this.db.deRegisterForGame(this.game.id).subscribe(
      (success: any) => {
        console.log(success);
    
        if (success.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: success.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else if (success.hasOwnProperty('success')) {
          if (success.success === true) {
            this.confirmationService.confirm({
              header: 'Success',
              message: 'Successfully de-registered from game!',
              accept: () => {}
            });
          } else {
            this.confirmationService.confirm({
              header: 'Error',
              message: 'Failed to de-register for game',
              icon: 'pi pi-exclamation-triangle',
              accept: () => {}
            });
          }
        }

      }, (failure) => {
        console.error(failure);
        if (failure.hasOwnProperty('errorMsg')) {
          this.confirmationService.confirm({
            header: 'Error',
            message: failure.errorMsg,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        } else {
          this.confirmationService.confirm({
            header: 'Error',
            message: 'Unknown error',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      },
      () => {
        this.refreshGame();
      }
    );
  }
}

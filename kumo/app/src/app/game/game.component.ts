import { UserService } from './../user.service';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { DatabaseService } from '../database.service';
import { ConfirmationService } from 'primeng/api';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

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

  public selectedPlayer;
  public get allPlayers() {
    let ret = [];

    for (let i = 0; i < this.editedGame.players.length; ++i) {
      ret.push({label: this.game.players[i].name, value: {id: this.game.players[i].id, name: this.game.players[i].name}});
    }

    return ret;
  }

  public get isAdmin() {
    return this.us.isAdmin();
  }

  public editingEnabled = false;
  public registered = false;
  public displayDetails = false;
  public editedGame: any = {};
  public newDmName = '';
  public newDmId = '';
  public newSystemName = '';
  public newDay = '';
  public newTime = '';

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

  public gameSystems = [
    { label: 'New System', value: { id: 0, name: 'New System'}}
  ];

  public dms = [
    { label: 'New DM', value: { id: 0, name: 'New DM'}}
  ];

  public days = [
    { label: 'New Day', value: { id: 0, name: 'New Day'}}
  ];

  public times = [
    { label: 'New Time', value: { id: 0, name: 'New Time'}}
  ];

  public errorMessages = {
    name: '',
    dm: '',
    system: '',
    day: '',
    time: '',
    description: '',
    registered: '',
    waitlist: ''
  };

  constructor(private db: DatabaseService,
    private us: UserService,
    private confirmationService: ConfirmationService,
    private fb: FormBuilder) {
      setTimeout(() => this.checkRegistration(), 500);
    }

  ngOnInit() {
  }

  public validateFields() {
    let pass = true;

    this.errorMessages.name = '';
    this.errorMessages.dm = '';
    this.errorMessages.system = '';
    this.errorMessages.day = '';
    this.errorMessages.time = '';
    this.errorMessages.description = '';
    this.errorMessages.registered = '';
    this.errorMessages.waitlist = '';

    if (this.editedGame.name.length === 0) {
      this.errorMessages.name = 'You must provide a name';
      pass = false;
    }

    if (this.editedGame.dm.id === 0) {
      if (this.newDmName.length === 0) {
        this.errorMessages.dm = '<div>You must provide a DM Name</div>';
        pass = false;
      }

      if (this.newDmId.length === 0) {
        this.errorMessages.dm += '<div>You must provide a DM Kumo ID</div>';
        pass = false;
      }
    }

    if (this.editedGame.system.id === 0) {
      if (this.newSystemName.length === 0) {
        this.errorMessages.system = 'You must provide a System Name';
        pass = false;
      }
    }

    if (this.editedGame.day.id === 0) {
      if (this.newDay.length === 0) {
        this.errorMessages.day = 'You must provide a Day Name';
        pass = false;
      }
    }

    if (this.editedGame.time.id === 0) {
      if (this.newTime.length === 0) {
        this.errorMessages.time = 'You must provide a Time Name';
        pass = false;
      }
    }

    if (!this.editedGame.description) {
      this.errorMessages.description = 'You must provide a Description';
      pass = false;
    }
    if (this.editedGame.description.length === 0) {
      this.errorMessages.description = 'You must provide a Description';
      pass = false;
    }

    if (this.editedGame.seats.length === 0) {
      this.errorMessages.registered = 'You must provide a number of seats';
      pass = false;
    } else if (isNaN(this.editedGame.seats)) {
      this.errorMessages.registered = 'You must provide a number of seats';
      pass = false;
    }
    
    if (this.editedGame.waitlist.length === 0) {
      this.errorMessages.waitlist = 'You must provide a number of waitlist';
      pass = false;
    } else if (isNaN(this.editedGame.waitlist)) {
      this.errorMessages.waitlist = 'You must provide a number of waitlist';
      pass = false;
    }

    return pass;
  }

  public enableEditing() {
    this.editingEnabled = true;
    Object.assign(this.editedGame, this.game);

    this.db.getGameSystems().subscribe(
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
          this.gameSystems = [
            { label: 'New System', value: { id: 0, name: 'New System'}}
          ];
          success.results.forEach((result) => {
            this.gameSystems.push({label: result.name, value: { id: result.id, name: result.name }});
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
            message: 'Unknown error occured',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      }, () => {

      }
    );

    this.db.getDungeonMasters().subscribe(
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
          this.dms = [
            { label: 'New DM', value: { id: 0, name: 'New DM'}}
          ];
          success.results.forEach((result) => {
            this.dms.push({label: result.name, value: { id: result.id, name: result.name }});
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
            message: 'Unknown error occured',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }
      }, () => {

      }
    );

    this.db.getDays().subscribe(
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
          this.days = [
            { label: 'New Day', value: { id: 0, name: 'New Day'}}
          ];
          success.results.forEach((result) => {
            this.days.push({label: result.name, value: { id: result.id, name: result.name }});
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
            message: 'Unknown error occured',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }

      }, () => {

      }
    );

    this.db.getTimes().subscribe(
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
          this.times = [
            { label: 'New Time', value: { id: 0, name: 'New Time'}}
          ];
          success.results.forEach((result) => {
            this.times.push({label: result.name, value: { id: result.id, name: result.name }});
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
            message: 'Unknown error occured',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {}
          });
        }

      }, () => {

      }
    )
  }

  public cancelEdits() {
    this.editingEnabled = false;
    Object.assign(this.editedGame, this.game);
  }

  public saveEdits() {
    console.log(this.editedGame);
    if (this.validateFields()) {
      if (this.editedGame.system.id === 0) {
        this.editedGame.system.name = this.newSystemName;
      }
      if (this.editedGame.dm.id === 0) {
        this.editedGame.dm.id = this.newDmId;
        this.editedGame.dm.name = this.newDmName;
      }
      if (this.editedGame.day.id === 0) {
        this.editedGame.day.name = this.newDay;
      }
      if (this.editedGame.time.id === 0) {
        this.editedGame.time.name = this.newTime;
      }

      this.db.updateGameDetails(this.editedGame).subscribe(
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
            this.editingEnabled = false;
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
      )
    }
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

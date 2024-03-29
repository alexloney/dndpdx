import { DatabaseService } from './../database.service';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { timeout } from 'rxjs/operators';

@Component({
  selector: 'app-gamelist',
  templateUrl: './gamelist.component.html',
  styleUrls: ['./gamelist.component.scss']
})
export class GamelistComponent implements OnInit, OnChanges {

  @Input() filters: string;
  @Input() mygames: boolean;

  private _filters: any = {};

  ngOnChanges(changes) {
    if (changes.hasOwnProperty('filters')) {
      try {
        this._filters = JSON.parse(changes.filters.currentValue);
        console.log(this._filters);
        this.applyFilters();
      } catch (e) {
        if (e instanceof SyntaxError) {
          // error?
        } else {
          console.error(e);
        }
      }
    } else if (changes.hasOwnProperty('mygames')) {
      console.log(changes);

      this.getGames();
    }
  }


  // @Input('filters') set filters(value: string) {
  //   try {
  //   this._filters = JSON.parse(value)
  //   this.applyFilters();
  //   } catch (e) {
  //     if (e instanceof SyntaxError) {
  //       // TODO: Do nothing
  //     } else {
  //       // TODO: Do something with the error
  //     }
  //   }
  // }

  public games: any = [];

  constructor(private db: DatabaseService) {
    this.getGames();
  }

  ngOnInit() {
  }

  private getGames() {
    this.db.getAllGames(this.mygames).subscribe(
      (success: any) => {
        if (success.hasOwnProperty('errorMsg')) {
          console.error(success);
          // TODO: Display error message

          return;
        }

        this.games = success.results;
        for (let game of this.games) {
          game.visible = true;
        }
        /*
        for (let game of this.games) {
          game.seated = [];
          game.waiting = [];

          for (let i = 0; i < game.players.length; ++i) {
            if (i < game.seats) {
              game.seated.append(game.players[i]);
            } else {
              game.waiting.append(game.players[i]);
            }
          }
        }
        */
      },
      (failure) => {

      },
      () => {}
    );
  }

  private applyFilters() {
    console.log('Filtering games...');
    for (let i = 0; i < this.games.length; ++i) {
      let visible = true;
      if (this._filters.dm.id !== 0) {
        if (this.games[i].dm.id !== this._filters.dm.id) {
          visible = false;
        }
      }
      if (this._filters.gameSystem.id !== 0) {
        if (this.games[i].system.id !== this._filters.gameSystem.id) {
          visible = false;
        }
      }
      if (this._filters.startDay.id !== 0) {
        if (this.games[i].day.id < this._filters.startDay.id) {
          visible = false;
        }
      }
      if (this._filters.endDay.id !== 0) {
        if (this.games[i].day.id > this._filters.endDay.id) {
          visible = false;
        }
      }
      if (this._filters.startTime.id !== 0) {
        if (this.games[i].time.id < this._filters.startTime.id) {
          visible = false;
        }
      }
      if (this._filters.endTime.id !== 0) {
        if (this.games[i].time.id > this._filters.endTime.id) {
          visible = false;
        }
      }

      console.log('Visible: ' + visible);
      this.games[i].visible = visible;
    }
  }

  public refreshGame(game) {
    console.log('Refreshing ' + game.id);

    for(let i = 0; i < this.games.length; ++i) {
      if (this.games[i].id === game.id) {
        Object.assign(this.games[i], game);
        break;
      }
    }
  }

}

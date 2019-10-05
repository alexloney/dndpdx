import { Component, OnInit, Input } from '@angular/core';
import { DatabaseService } from '../database.service';
import { ConfirmationService } from 'primeng/api';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  @Input() game: any;

  public displayDetails = false;
  
  constructor(private db: DatabaseService,
    private confirmationService: ConfirmationService) { }

  ngOnInit() {
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
        // TODO: Refresh game data
      }
    );
  }
}

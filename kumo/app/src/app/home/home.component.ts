import { ConfirmationService } from 'primeng/api';
import { DatabaseService } from './../database.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  public userid;
  public displayLogin = false;
  public loading = false;

  constructor(private ds: DatabaseService,
    private confirmationService: ConfirmationService) { }

  ngOnInit() {
  }

  public showLogin() {
    this.displayLogin = true;
  }

  public loginWithId() {
    this.loading = true;
    this.ds.isIdValid(this.userid).subscribe((success) => {
      this.confirmationService.confirm({
        message: 'Message',
        accept: () => {
          // Stuff
        }
      });
      console.log(success);
    }, (failure) => {
      console.error(failure);
    }, () => {
      this.loading = false;
    });
  }

}

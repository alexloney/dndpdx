import { ConfirmationService } from 'primeng/api';
import { DatabaseService } from '../database.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  public userid = '';
  public name = '';
  public displayLogin = false;
  public loading = false;
  public displayName = false;

  constructor(private ds: DatabaseService,
    private confirmationService: ConfirmationService,
    private router: Router) { }

  ngOnInit() {
  }

  public showLogin() {
    this.displayLogin = true;
    this.displayName = false;
  }

  public loginWithId() {

    if (this.userid.length === 0) {
      this.confirmationService.confirm({
        message: 'Please provide an ID',
        accept: () => {}
      });
      return;
    }

    this.loading = true;
    this.ds.isIdValid(this.userid).subscribe((success) => {
      if (success.hasOwnProperty('errorMsg')) {
        if (success.errorMsg === 'User not registered') {
          this.displayName = true;
        } else {
          this.confirmationService.confirm({
            message: success.errorMsg,
            accept: () => {}
          });
        }
      } else {
        if (success.hasOwnProperty('sessionId')) {
          this.ds.setSessionId(success.sessionId);
          this.router.navigate(['/home']);
        }
      }
      console.log(success);
    }, (failure) => {
      console.error(failure);
    }, () => {
      this.loading = false;
    });
  }

  public register() {

    if (this.name.length === 0) {
      this.loginWithId();
      return;
    }

    if (this.userid.length === 0) {
      this.confirmationService.confirm({
        message: 'Please provide an ID',
        accept: () => {}
      });
      return;
    }

    this.loading = true;
    this.ds.register(this.userid, this.name).subscribe((success: any) => {
      if (success.hasOwnProperty('sessionId')) {
        this.ds.setSessionId(success.sessionId);
        this.router.navigate(['/home']);
      }
    }, (failure) => {
      console.error(failure);
    }, () => {
      this.loading = false;
    });
  }

}

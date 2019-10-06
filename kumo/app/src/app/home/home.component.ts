import { Router } from '@angular/router';
import { ConfirmationService } from 'primeng/api';
import { DatabaseService } from './../database.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  public filters: string = '';
  public myGames = false;

  constructor(private ds: DatabaseService,
    private confirmationService: ConfirmationService,
    private router: Router) {
      // setTimeout(() => {
      //   console.log(this.filters);
      // }, 10000);
    }

  ngOnInit() {
  }

  public logout() {
    this.ds.logout().subscribe(
      () => {},
      () => {},
      () => {
        this.ds.setSessionId('');
        this.router.navigate(['/']);
      }
    );
  }

  public updateFilters(f) {
    console.log(f);
  }

  public showMyGames() {
    this.myGames = true;
  }

  public showAllGames() {
    this.myGames = false;
  }
}

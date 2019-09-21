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

  public filters = {};

  constructor(private ds: DatabaseService,
    private confirmationService: ConfirmationService,
    private router: Router) { }

  ngOnInit() {
  }

  public updateFilters(e) {
    this.filters = e;
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
}

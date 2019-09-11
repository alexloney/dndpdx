import { DatabaseService } from './../database.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  public userid;

  constructor(private ds: DatabaseService) { }

  ngOnInit() {
  }

  public loginWithId(e) {
    this.ds.isIdValid(this.userid).subscribe((success) => {
      console.log(success);
    });
  }

}

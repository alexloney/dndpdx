import { Component, OnInit, Input } from '@angular/core';
import { timeout } from 'rxjs/operators';

@Component({
  selector: 'app-gamelist',
  templateUrl: './gamelist.component.html',
  styleUrls: ['./gamelist.component.scss']
})
export class GamelistComponent implements OnInit {

  @Input() filters: any = {};

  constructor() {
    setTimeout(() => {
      console.log(this.filters);
    }, 5000);
  }

  ngOnInit() {
  }

}

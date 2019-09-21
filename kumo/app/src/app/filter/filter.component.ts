import { DatabaseService } from './../database.service';
import { Component, OnInit, Input, Output } from '@angular/core';
import { EventEmitter } from '@angular/core';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {

  @Input() filters: any = {};
  @Output() filtersChange = new EventEmitter();

  public gameSystems = [
    { label: 'All Systems', value: { id: 0, name: 'All Systems'}}
  ];

  public dms = [
    { label: 'All DMs', value: { id: 0, name: 'All DMs'}}
  ];

  public days = [
    { label: 'All Days', value: { id: 0, name: 'All Days'}}
  ];

  public times = [
    { label: 'All Times', value: { id: 0, name: 'All Times'}}
  ];

  constructor(private db: DatabaseService) {
    
    setTimeout(() => {
      this.filters.gameSystem = '';
      this.filters.dm = '';
      this.filters.startDay = '';
      this.filters.endDay = '';
      this.filters.startTime = '';
      this.filters.endTime = '';
      this.filtersChange.emit(this.filters);
    }, 3000);
  }

  ngOnInit() {
    this.populateDropdowns();
  }

  private populateDropdowns() {
    this.db.getGameSystems().subscribe(
      (success) => {
        console.log(success);
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );
    
    this.db.getDungeonMasters().subscribe(
      (success) => {
        console.log(success);
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );

    this.db.getDays().subscribe(
      (success: any) => {
        if (success.hasOwnProperty('errorMsg')) {
          console.error(success);
          // TODO: Display error message

          return;
        }

        this.days = [
          { label: 'All Days', value: { id: 0, name: 'All Days'}}
        ];
        success.results.forEach((result) => {
          this.days.push({label: result.name, value: { id: result.id, name: result.name }});
        });
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );
    
    this.db.getTimes().subscribe(
      (success) => {
        console.log(success);
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );
  }

}

import { DatabaseService } from './../database.service';
import { Component, OnInit, Input, Output } from '@angular/core';
import { DoCheck, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {

  @Input() filters: any = {};
  @Output() filtersChange = new EventEmitter();

  get gameSystem() {
    return this.filters.gameSystem;
  }
  set gameSystem(value) {
    this.filters.gameSystem = value;
    this.filtersChange.emit(this.filters);
  }

  get dm() {
    return this.filters.dm;
  }
  set dm(value) {
    this.filters.dm = value;
    this.filtersChange.emit(this.filters);
  }

  get startDay() {
    return this.filters.startDay;
  }
  set startDay(value) {
    this.filters.startDay = value;
    this.filtersChange.emit(this.filters);
  }

  get endDay() {
    return this.filters.endDay;
  }
  set endDay(value) {
    this.filters.endDay = value;
    this.filtersChange.emit(this.filters);
  }

  get startTime() {
    return this.filters.startTime;
  }
  set startTime(value) {
    this.filters.startTime = value;
    this.filtersChange.emit(this.filters);
  }

  get endTime() {
    return this.filters.endTime;
  }
  set endTime(value) {
    this.filters.endTime = value;
    this.filtersChange.emit(this.filters);
  }

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
      this.gameSystem = this.gameSystems[0].value;
      this.dm = this.dms[0].value;
      this.startDay = this.days[0].value;
      this.endDay = this.days[0].value;
      this.startTime = this.times[0].value;
      this.endTime = this.times[0].value;
    });
  }

  ngOnInit() {
    this.populateDropdowns();
  }

  private populateDropdowns() {
    this.db.getGameSystems().subscribe(
      (success: any) => {
        if (success.hasOwnProperty('errorMsg')) {
          console.error(success);
          // TODO: Display error message

          return;
        }

        this.gameSystems = [
          { label: 'All Systems', value: { id: 0, name: 'All Systems'}}
        ];
        success.results.forEach((result) => {
          this.gameSystems.push({label: result.name, value: { id: result.id, name: result.name }});
        });
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );
    
    this.db.getDungeonMasters().subscribe(
      (success: any) => {
        if (success.hasOwnProperty('errorMsg')) {
          console.error(success);
          // TODO: Display error message

          return;
        }

        this.dms = [
          { label: 'All DMs', value: { id: 0, name: 'All DMs'}}
        ];
        success.results.forEach((result) => {
          this.dms.push({label: result.name, value: { id: result.id, name: result.name }});
        });
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
      (success: any) => {
        if (success.hasOwnProperty('errorMsg')) {
          console.error(success);
          // TODO: Display error message

          return;
        }

        this.times = [
          { label: 'All Times', value: { id: 0, name: 'All Times'}}
        ];
        success.results.forEach((result) => {
          this.times.push({label: result.name, value: { id: result.id, name: result.name }});
        });
      },
      (failure) => {
        console.error(failure);
      },
      () => {

      }
    );
  }

}

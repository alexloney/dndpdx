import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';
import { environment } from './../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private endpoint = environment.apiUrl;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };
  private httpFormOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    })
  };
  private sessionId = '';

  constructor(private http: HttpClient) { }

  private getHeaders(type) {
    let headers: any = {};

    if (type === 'json') {
      headers['Content-Type'] = 'application/json';
    } else if (type === 'form') {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
    }

    if (this.sessionId !== null && this.sessionId.length > 0) {
      headers['Authorization'] = this.sessionId;
    }

    return { 'headers': new HttpHeaders(headers) };
  }

  public setSessionId(sessionid) {
    this.sessionId = sessionid;
  }

  public register(id, name) {
    return this.http.post(this.endpoint + 'players/register', 'id=' + id + '&name=' + name, this.getHeaders('form'));
  }

  public logout() {
    return this.http.post(this.endpoint + 'logout', this.getHeaders('json'));
  }

  public getGameSystems() {
    return this.http.get(this.endpoint + 'search/systems', this.getHeaders('json'));
  }

  public getDungeonMasters() {
    return this.http.get(this.endpoint + 'search/dms', this.getHeaders('json'));
  }

  public getDays() {
    return this.http.get(this.endpoint + 'search/days', this.getHeaders('json'));
  }

  public getTimes() {
    return this.http.get(this.endpoint + 'search/times', this.getHeaders('json'));
  }

  private extractData(res: Response) {
    let body = res;
    return body || { };
  }

  isIdValid(id): Observable<any> {
    return this.http.get(this.endpoint + 'players/' + id, this.getHeaders('json')).pipe(map(this.extractData));
  }
}

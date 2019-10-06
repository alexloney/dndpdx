import { ConfirmationService } from 'primeng/api';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';
import { environment } from './../environments/environment';
import { SelectControlValueAccessor } from '@angular/forms';

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

  constructor(private http: HttpClient,
    private confirmationService: ConfirmationService) { }


  public handleDatabaseResponse(resp) {
    if (resp.hasOwnProperty('errorMsg')) {
      this.confirmationService.confirm({
        header: 'Error',
        icon: 'pi pi-exclamation-triangle',
        message: resp.errorMsg,
        accept: () => {}
      });
      return false;
    } else if (resp.hasOwnProperty('success')) {
      return resp.success;
    }

    return resp;
  }

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
    return this.http.post(this.endpoint + 'logout', null, this.getHeaders('json'));
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

  public getAllGames(mygames) {
    if (mygames) {
      return this.http.get(this.endpoint + 'games/mine', this.getHeaders('json'));
    }

    return this.http.get(this.endpoint + 'games/all', this.getHeaders('json'));
  }

  public registerForGame(id) {
    return this.http.post(this.endpoint + 'games/register/' + id, null, this.getHeaders('json'))
  }

  public getGameById(id) {
    return this.http.get(this.endpoint + 'games/id/' + id, this.getHeaders('json'));
  }

  public isRegistered(id) {
    return this.http.get(this.endpoint + 'games/registered/' + id, this.getHeaders('json'));
  }

  public deRegisterForGame(id) {
    return this.http.post(this.endpoint + 'games/deregister/' + id, null, this.getHeaders('json'));
  }

  private extractData(res: Response) {
    let body = res;
    return body || { };
  }



  isIdValid(id): Observable<any> {
    return this.http.get(this.endpoint + 'players/' + id, this.getHeaders('json')).pipe(map(this.extractData));
  }
}

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

  public setSessionId(sessionid) {
    this.sessionId = sessionid;
  }

  public register(id, name) {
    return this.http.post(this.endpoint + 'players/register', 'id=' + id + '&name=' + name, this.httpFormOptions);
  }

  private extractData(res: Response) {
    let body = res;
    return body || { };
  }

  isIdValid(id): Observable<any> {
    return this.http.get(this.endpoint + 'players/' + id).pipe(map(this.extractData));
  }
}

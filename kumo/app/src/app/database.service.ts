import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private endpoint = 'http://127.0.0.1:5002/';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(private http: HttpClient) { }

  private extractData(res: Response) {
    let body = res;
    return body || { };
  }

  isIdValid(id): Observable<any> {
    return this.http.get(this.endpoint + 'users/' + id).pipe(map(this.extractData));
  }
}

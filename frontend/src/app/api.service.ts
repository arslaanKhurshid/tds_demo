import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

interface Log {
  id: string;
  timestamp: string;
  source_ip: string;
  event_type: string;
  details: { [key: string]: string };
}

interface Rule {
  id: string;
  name: string;
  query: string;
  exclusion_list: string[];
  enabled: boolean;
}

interface Alert {
  id: string;
  rule_id: string;
  severity: string;
  details: { [key: string]: string };
  timestamp: string;
}

interface ApiResponse {
  message: string;
  [key: string]: any;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Logs
  getLogs(): Observable<Log[]> {
    return this.http.get<Log[]>(`${this.apiUrl}/logs`).pipe(
      catchError(this.handleError)
    );
  }

  createMockLog(): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/logs/mock`, {}).pipe(
      catchError(this.handleError)
    );
  }

  // Rules
  getRules(): Observable<Rule[]> {
    return this.http.get<Rule[]>(`${this.apiUrl}/rules`).pipe(
      catchError(this.handleError)
    );
  }

  generateRule(): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/rules/generate`, {}).pipe(
      catchError(this.handleError)
    );
  }

  // Alerts
  getAlerts(): Observable<Alert[]> {
    return this.http.get<Alert[]>(`${this.apiUrl}/alerts`).pipe(
      catchError(this.handleError)
    );
  }

  detectThreats(ruleId: string): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/alerts/detect`, { rule_id: ruleId }).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An error occurred';
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
      if (error.error?.detail) {
        errorMessage += `\nDetail: ${error.error.detail}`;
      }
    }
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
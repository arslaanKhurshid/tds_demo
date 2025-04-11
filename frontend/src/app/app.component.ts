import { Component, OnInit } from '@angular/core';
import { ApiService } from './api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [CommonModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'Threat Detection System';
  activeTab: string = 'logs';
  logs: any[] = [];
  rules: any[] = [];
  alerts: any[] = [];
  errorMessage: string = '';
  successMessage: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadLogs();
    this.loadRules();
    this.loadAlerts();
  }

  setActiveTab(tab: string) {
    this.activeTab = tab;
    this.errorMessage = '';
    this.successMessage = '';
  }

  toggleTheme() {
    document.body.classList.toggle('dark-theme');
  }

  loadLogs() {
    this.apiService.getLogs().subscribe({
      next: (logs) => {
        this.logs = logs;
      },
      error: (err) => {
        this.errorMessage = 'Failed to load logs: ' + err.message;
      }
    });
  }

  createMockLog() {
    this.apiService.createMockLog().subscribe({
      next: (response) => {
        this.successMessage = response.message;
        this.loadLogs();
      },
      error: (err) => {
        this.errorMessage = 'Failed to create mock log: ' + err.message;
      }
    });
  }

  loadRules() {
    this.apiService.getRules().subscribe({
      next: (rules) => {
        this.rules = rules;
      },
      error: (err) => {
        this.errorMessage = 'Failed to load rules: ' + err.message;
      }
    });
  }

  generateRule() {
    this.apiService.generateRule().subscribe({
      next: (response) => {
        this.successMessage = response.message;
        this.loadRules();
      },
      error: (err) => {
        this.errorMessage = 'Failed to generate rule: ' + err.message;
      }
    });
  }

  loadAlerts() {
    this.apiService.getAlerts().subscribe({
      next: (alerts) => {
        this.alerts = alerts;
      },
      error: (err) => {
        this.errorMessage = 'Failed to load alerts: ' + err.message;
      }
    });
  }

  detectThreats(ruleId: string) {
    if (!ruleId) return;
    this.apiService.detectThreats(ruleId).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        this.loadAlerts();
      },
      error: (err) => {
        this.errorMessage = 'Failed to detect threats: ' + err.message;
      }
    });
  }
}
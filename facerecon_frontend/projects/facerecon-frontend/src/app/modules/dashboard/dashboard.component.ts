import { Component, OnInit } from '@angular/core';

import { KeycloakService } from 'keycloak-angular';
import { KeycloakProfile } from 'keycloak-js';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {


  title = 'Facerecon Dashboard';
  public userProfile: KeycloakProfile | null = null;

  constructor(
    private readonly keycloakService: KeycloakService
  ) { }

  ngOnInit(): void {
    this.keycloakService.loadUserProfile().then(profile => {
      this.userProfile = profile;
    });
  }

  accountManagement() {
    this.keycloakService.getKeycloakInstance().accountManagement();
  }
  logout() {
    this.keycloakService.logout();
  }

}

import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { KeycloakAuthGuard, KeycloakService } from 'keycloak-angular';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationGuard extends KeycloakAuthGuard {

  constructor(
    protected readonly router: Router,
    protected readonly keycloakService: KeycloakService
  ) {
    super(router, keycloakService);
  }

  isAccessAllowed(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean | UrlTree> {

    return new Promise(async (resolve, reject) => {
      // Force the user to log in if currently unauthenticated.
      if (!this.authenticated) {
        await this.keycloakService.login({
          redirectUri: window.location.origin + state.url,
        });
      }

      console.log('role restriction given at app-routing.module for this route', route.data.roles);
      console.log('User roles coming after login from keycloak :', this.roles);

      // Get the roles required from the route.
      const requiredRoles = route.data.roles;
      let granted: boolean = false;

      // Allow the user to to proceed if no additional roles are required to access the route.
      if (!(requiredRoles instanceof Array) || requiredRoles.length === 0) {
        granted = true;
      } else {

        for (const requiredRole of requiredRoles) {
          if (this.roles.indexOf(requiredRole) > -1) {
            granted = true;
            break;
          }
        }
      }
      if(granted === false) {
        this.router.navigate(['/not-authorized']);
      }
      resolve(granted);

      // Allow the user to proceed if all the required roles are present.
      //return requiredRoles.every((role) => this.roles.includes(role));
    });

  }

}

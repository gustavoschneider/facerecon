import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../../environments/environment';

import { Client } from '../classes/clients';

@Injectable({
  providedIn: 'root'
})
export class ClientsService {

  URL = environment.api.url + '/management/clients'
  constructor(
    private httpClient: HttpClient
  ) { }

  getClients(): Observable<Client[]> {
    return this.httpClient.get<Client[]>(this.URL);
  }

  getClient(keycloak_id: string): Observable<Client> {
    return this.httpClient.get<Client>(this.URL + '/' + keycloak_id);
  }

  saveClient(client: Client): Observable<Client> {
    client = Client.clean(client);

    if (client.hasOwnProperty('id') && client.id != null) {
      return this.httpClient.put<Client>(this.URL + '/' + client.keycloak_id, client);
    } else {
      return this.httpClient.post<Client>(this.URL, client);
    }
  }

  deleteClient(client: Client): Observable<Client> {
    return this.httpClient.delete(this.URL + '/' + client.keycloak_id);
  }

  getClientCredentials(client: Client): Observable<{client_id: string, client_secret: string}> {
    return this.httpClient.get<{client_id: string, client_secret: string}>(this.URL + '/'+ client.keycloak_id + '/credentials');

  }

}

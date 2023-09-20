import { Component, OnInit, AfterViewInit, ChangeDetectorRef } from '@angular/core';

import { merge, Observable } from 'rxjs';
import { delay, map, startWith, switchMap } from 'rxjs/operators';

import { MatDialog } from '@angular/material/dialog';

import { ClientsService } from '../../services/clients.service';
import { Client } from '../../classes/clients';

import { DeleteConfirmDialogComponent } from '../../components/delete-confirm-dialog/delete-confirm-dialog.component';
import { ClientDetailsDialogComponent } from '../../components/client-details-dialog/client-details-dialog.component';
import { CredentialsDialogComponent } from '../../components/credentials-dialog/credentials-dialog.component';

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.scss']
})
export class ClientsComponent implements OnInit, AfterViewInit {

  displayedColumns: string[] = ['client_id', 'client_name', 'client_description', 'created_at', 'actions'];
  resultsLength: number = 0;
  isLoadingResults: boolean = false;

  clientsData: Observable<Client[]> = new Observable<Client[]>();

  constructor(
    private matdialog: MatDialog,
    private clientsService: ClientsService,
    private changeDetectorRefs: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.getClients();
  }

  getClients() {
    this.clientsData = merge().pipe(
      startWith({}),
      delay(0),
      switchMap( () => {
        this.isLoadingResults = true;
        return this.clientsService.getClients();
      }),
      map( data => {
        this.isLoadingResults = false;
        this.resultsLength = data.length;
        return data;
      })
    );
    this.changeDetectorRefs.detectChanges();

  }

  createClient(): void {
    let createDialogRef = this.matdialog.open(
      ClientDetailsDialogComponent,
      {
        width: '500px',
        data: new Client()
      }
    );

    createDialogRef.afterClosed().subscribe((client_data: Client) => {
      if (client_data !== undefined) {
        this.clientsService.saveClient(client_data).subscribe((client_created: Client) => {
          if (client_created.hasOwnProperty('keycloak_id') && client_created.keycloak_id != null) {
            this.getClients();
          }
        });
      }

    });

  }
  editClient(client: Client): void {
    let editDialogRef = this.matdialog.open(
      ClientDetailsDialogComponent,
      {
        width: '500px',
        data: client
      }
    );

    editDialogRef.afterClosed().subscribe((client_data: Client) => {
      if (client_data !== undefined) {
        this.clientsService.saveClient(client_data).subscribe((client_edited: Client) => {
          if (client_edited.hasOwnProperty('keycloak_id') && client_edited.keycloak_id != null) {
            this.getClients();
          }
        });
      }
    });

  }
  getClientCredentials(client: Client): void {

    this.clientsService.getClientCredentials(client).subscribe(client_credentials => {

      let credentialsDialogRef = this.matdialog.open(
        CredentialsDialogComponent,
        {
          width: '500px',
          data: client_credentials
        }
      );

      credentialsDialogRef.afterClosed().subscribe(result => {
      });

    });

  }

  deleteClient(client: Client): void {
    let deleteDialogRef = this.matdialog.open(
      DeleteConfirmDialogComponent,
      {
        width: '500px',
        data: {
          title: 'Confirm delete?',
          message: 'The Client '+ client.client_name +' with clientId: '+ client.client_id +' will be deleted.',
          showDanger: true
        }
      }
    );

    deleteDialogRef.afterClosed().subscribe(result => {
      if(result === true) {
        this.clientsService.deleteClient(client).subscribe((client_deleted: Client) => {
          if (client_deleted.hasOwnProperty('id') && client_deleted.id != null) {
            this.getClients();
          }
        });
      }
    });

  }
}




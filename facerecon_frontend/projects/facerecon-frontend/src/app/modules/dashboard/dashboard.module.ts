import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DEFAULT_OPTIONS } from '@angular/material/dialog';

import { MaterialImportsModule } from '../material-imports/material-imports.module';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { HomeComponent } from './routes/home/home.component';
import { ClientsComponent } from './routes/clients/clients.component';
import { BillingComponent } from './routes/billing/billing.component';
import { DeleteConfirmDialogComponent } from './components/delete-confirm-dialog/delete-confirm-dialog.component';
import { ClientDetailsDialogComponent } from './components/client-details-dialog/client-details-dialog.component';
import { CredentialsDialogComponent } from './components/credentials-dialog/credentials-dialog.component';


@NgModule({
  declarations: [
    HomeComponent,
    DashboardComponent,
    ClientsComponent,
    BillingComponent,
    DeleteConfirmDialogComponent,
    ClientDetailsDialogComponent,
    CredentialsDialogComponent
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    MaterialImportsModule
  ],
  entryComponents: [
    DeleteConfirmDialogComponent,
    ClientDetailsDialogComponent
  ],
  providers: [
    { provide: MAT_DIALOG_DEFAULT_OPTIONS, useValue: { hasBackdrop: false }}
  ]
})
export class DashboardModule { }

import { Component, Inject, OnInit } from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-credentials-dialog',
  templateUrl: './credentials-dialog.component.html',
  styleUrls: ['./credentials-dialog.component.scss']
})
export class CredentialsDialogComponent implements OnInit {

  client_secret_password: boolean = true;

  constructor(@Inject(MAT_DIALOG_DATA) public data: {client_id: string, client_secret: string}) { }

  ngOnInit(): void {
  }

  toggleClientSecretPassword() {
    this.client_secret_password = !this.client_secret_password;
  }

}

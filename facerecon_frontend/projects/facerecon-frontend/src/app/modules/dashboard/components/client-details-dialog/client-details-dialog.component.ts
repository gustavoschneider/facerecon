import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Client } from '../../classes/clients';

@Component({
  selector: 'app-client-details-dialog',
  templateUrl: './client-details-dialog.component.html',
  styleUrls: ['./client-details-dialog.component.scss']
})
export class ClientDetailsDialogComponent implements OnInit {

  action: string = 'Create';

  clientForm: FormGroup = this.formBuilder.group({
    id: [null],
    keycloak_id: [null],
    user_id: [null],
    client_id: ['', [Validators.required]],
    client_name: ['', [Validators.required]],
    client_description: [''],
    client_redirecturis: ['', [Validators.required]],
    client_weborigins: ['', [Validators.required]],
    deleted: [null],
    created_at: [null],
    modified_at: [null]
  });

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<ClientDetailsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Client
  ) {
    if (this.data.hasOwnProperty('id')) {
      this.action = 'Edit';
      this.clientForm.patchValue(this.data);
    }
  }

  ngOnInit(): void {

  }

  onSubmit(): void {
    if(this.clientForm.valid) {
      this.dialogRef.close(this.clientForm.value);
    }
  }



}

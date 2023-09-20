import * as moment from 'moment';

import { BaseObject } from './base-object';

export class Client extends BaseObject {
  id?: number;
  keycloak_id?: string;
  user_id?: string;

  client_id?: string;
  client_name?: string;
  client_description?: string;

  client_redirecturis?: string;
  client_weborigins?: string;

  deleted?: boolean;
  created_at?: moment.Moment;
  modified_at?: moment.Moment;

  constructor(data?: any) {
    super();

    if (data?.id) this.id = +data.id;
    if (data?.keycloak_id) this.keycloak_id = data.keycloak_id;
    if (data?.user_id) this.user_id = data.user_id;

    if (data?.client_id) this.client_id = data.client_id;
    if (data?.client_name) this.client_name = data.client_name;
    if (data?.client_description) this.client_description = data.client_description;

    if (data?.client_redirecturis) this.client_redirecturis = data.client_redirecturis;
    if (data?.client_weborigins) this.client_weborigins = data.client_weborigins;

    if (data?.deleted == true) this.deleted = true;
    if (data?.deleted == false) this.deleted = false;
    if (data?.created_at) this.created_at = moment(data.created_at);
    if (data?.modified_at) this.modified_at = moment(data.modified_at);
  }

  toString() {
    return `< Client(
      id="${this.id}",
      keycloak_id="${this.keycloak_id}",
      user_id="${this.user_id}",
      client_id="${this.client_id}",
      client_name="${this.client_name}",
      client_description="${this.client_description}",
      client_redirecturis="${this.client_redirecturis}",
      client_weborigins="${this.client_weborigins}",
      deleted="${this.deleted}",
      created_at="${this.created_at}",
      modified_at="${this.modified_at}"
      ) >`;
  }

}


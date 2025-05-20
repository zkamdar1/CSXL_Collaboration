/*
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Announcement } from '../announcement.model';
import { Observable, of } from 'rxjs';
//import { PermissionService } from 'src/app/permission.service';

/** Injects the event's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['announcement'].headline;
};

@Component({
  selector: 'app-announcement-details',
  templateUrl: './announcement-details.component.html',
  styleUrls: ['./announcement-details.component.css']
})
export class AnnouncementDetailsComponent {
  public static Route = {
    path: ':slug',
    title: 'Announcement Details',
    component: AnnouncementDetailsComponent
  };
  public announcement!: Announcement;

  constructor(
    private route: ActivatedRoute //private permission: PermissionService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      //profile: Profile;
      announcement: Announcement;
    };
    //this.profile = data.profile;
    this.announcement = data.announcement;

    // Admin Permission if has the actual permission or is event organizer
  }
}

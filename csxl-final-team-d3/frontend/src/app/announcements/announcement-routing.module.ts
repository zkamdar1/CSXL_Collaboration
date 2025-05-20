// announcement-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnnouncementsComponent } from './announcements-start/announcements.component';
import { CreateAnnouncementsComponent } from './create-announcements/create-announcements.component';
import { AnnouncementDetailsComponent } from './announcement-details/announcement-detail.component';

const routes: Routes = [
  AnnouncementsComponent.Route,
  // { path: 'announcement/edit/:slug', component: CreateAnnouncementsComponent }
  CreateAnnouncementsComponent.Route,
  AnnouncementDetailsComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AnnouncementRoutingModule {}

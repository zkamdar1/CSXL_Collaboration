import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Angular Material Modules */
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';

/* UI Widgets */
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { AnnouncementsComponent } from './announcements-start/announcements.component';
import { CreateAnnouncementsComponent } from './create-announcements/create-announcements.component';
import { AnnouncementRoutingModule } from './announcement-routing.module';
import { AnnouncementCard } from './widgets/announcement-card/announcement-card.widget';
import { AnnouncementList } from './widgets/announcement-list/announcement-list.widget';
import { AnnouncementDetailCard } from './widgets/announcement-detail-card/announcement-detail.widget';
import { AnnouncementDetailsComponent } from './announcement-details/announcement-detail.component';

@NgModule({
  declarations: [
    AnnouncementsComponent,
    CreateAnnouncementsComponent,
    AnnouncementCard,
    AnnouncementList,
    AnnouncementDetailCard,
    AnnouncementDetailsComponent
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
    MatChipsModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule,
    RouterModule,
    SharedModule,
    AnnouncementRoutingModule
  ]
})
export class AnnouncementsModule {}

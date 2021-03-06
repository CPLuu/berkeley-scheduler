///<reference path="../lib/polyfills.ts" />
import {Identifiable} from '../utils';
import Meeting from './meeting';


export interface Commitment extends Identifiable {
  id: string;
  color: string;

  // add(): void;
  // drop(): void;

  getName(): string;

  optionTypes: string[];
  getOptions(): Option[];
  getOptionsByType(type: string): Option[];
}

export interface Option extends Identifiable {
  type: string;
  selected: boolean;
  owner: Commitment;

  meetings: Meeting<Option>[];
}

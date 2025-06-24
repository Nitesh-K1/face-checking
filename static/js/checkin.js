// import { html, css, LitElement } from 'https://unpkg.com/lit@2.8.0/index.js?module';
// class CheckinTable extends LitElement {
//   static styles = css`
//     table { width: 100%; border-collapse: collapse; }
//     th, td { border: 1px solid #ddd; padding: 8px; }
//     th { background-color: #f2f2f2; }
//   `;
//   static properties = {
//     checkins: { type: Array }
//   };
//   constructor() {
//     super();
//     this.checkins = [];
//   }
//   connectedCallback() {
//     super.connectedCallback();
//     fetch('/api/checkins')
//       .then(res => res.json())
//       .then(data => this.checkins = data);
//   }
//   render() {
//     return html`
//       <table>
//         <thead>
//           <tr>
//             <th>Name</th>
//             <th>Date</th>
//             <th>Time</th>
//           </tr>
//         </thead>
//         <tbody>
//           ${this.checkins.map(entry => html`
//             <tr>
//               <td>${entry.name}</td>
//               <td>${entry.date}</td>
//               <td>${entry.time}</td>
//             </tr>
//           `)}
//         </tbody>
//       </table>
//     `;
//   }
// }
// customElements.define('checkin-table', CheckinTable);

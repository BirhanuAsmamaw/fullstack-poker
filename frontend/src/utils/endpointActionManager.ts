export default function endpointActionManager(action : string, value? : number) {
    let endpoint = ''
    let displayAction = ''
    switch (action) {
        case 'f':
          endpoint = '/hand/action/fold';
          displayAction = 'folds';
          break;
        case 'x':
          endpoint = '/hand/action/check_or_call';
          displayAction = 'checks';
          break;
        case 'c':
          endpoint = '/hand/action/check_or_call';
          displayAction = 'calls';
          break;
        case 'b':
          endpoint = '/hand/action/complete_bet_or_raise_to';
          displayAction = `bets ${value} chips`;
          break;
        case 'r':
          endpoint = '/hand/action/complete_bet_or_raise_to';
          displayAction = `raises to ${value} chips`;
          break;
        case 'allin':
          endpoint = '/hand/action/allin';
          displayAction = 'goes all-in';
          break;
        default:
          break;
      }

    return [endpoint, displayAction]
}
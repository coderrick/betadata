import React from "react";
import PropTypes from "prop-types";
import "./App.css";
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import { withStyles } from "@material-ui/core/styles";
import { DropzoneArea } from "material-ui-dropzone";
//Page Templates:
import Header from "./Header";
import DataForm from "./DataForm";
import SeekerVidSearch from "./SeekerVidSearch";

class UploadPage extends React.Component {
  state = {
    files: []
  };

  handleChange(files) {
    this.setState({
      files: files
    });
  }

  render() {
    const { classes } = this.props;

    return (
      <div className="upload-page">
        <Header />
        {/* <Button variant="contained" color="default" className={classes.button}>
          Upload
          <CloudUploadIcon className={classes.rightIcon} />
        </Button> */}
        <DropzoneArea onChange={this.handleChange.bind(this)} />
        <DataForm />
        <SeekerVidSearch/>
      </div>  
    );
  }
}

const styles = theme => ({
  button: {
    margin: theme.spacing.unit
  },
  leftIcon: {
    marginRight: theme.spacing.unit
  },
  rightIcon: {
    marginLeft: theme.spacing.unit
  },
  iconSmall: {
    fontSize: 20
  }
});

UploadPage.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(UploadPage);
